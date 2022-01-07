#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" JSON Parser to both validate and process the JSON String to a Python-understandable structure
    Spaces, tabs and line-breaks are allowed in input and will be ignored

    Validate and Parse JSON String by importing Parser to continue with processed output
        from JsonParser import JSONParser
        output = JSONParser( '{ "Name": "Reinier", "Age": 30.5 }' ).parse()
        print( output[ 'Name'] )

    Validate JSON String via command line - as return is impossible
        $ python JsonParser.py "{ \"Name\": \"Reinier\", \"Age\": 30.5 }"

    Author: Reinier van den Assum (reinier@foxy-solutions.com)
    Date: January 2022
"""
import sys
import re

class JSONParser:
    __originalString = ""
    __remainingChars = []
    
    __requiresSeparator = False
    __lastWasComma = False
    
    global CHARS
    CHARS = { 'object': { 'open': '{', 'close': '}' },
                'list': { 'open': '[', 'close': ']' },
                'attr': { 'open': '"', 'close': '"' },
                'sep': { 'attr': ',', 'decimal': '.' } }

    # parameterized constructor
    def __init__( self, jsonString ):
        # Save original string without line-breaks and tabs to allow better display in case of invalid JSON
        # Strip spaces in front and at the end, to avoid the main-while loops (object and list) to still have remainingChars, but only spaces
        # Convert to List as is more efficient than string manipulations
        self.__originalString = re.sub( r'\s{2,}', ' ', jsonString ).strip()
        self.__remainingChars = list( self.__originalString )

    """
        Initial parse method, which returns the JSON Object in Python types (dict or list)
    """
    def parse( self ):
        structure = None # define but not initiate as can be list or object

        # JSON is only valid when starts with object or list, thus { or [
        try:
            firstChar = self.__getNextChar()
            if firstChar == CHARS[ 'object' ][ 'open' ]:
                structure = self.__parseObject()
            elif firstChar == CHARS[ 'list' ][ 'open' ]:
                structure = self.__parseList()
            else:
                raise Exception( "JSON should start with " + CHARS[ 'object' ][ 'open' ] + " or " + CHARS[ 'list' ][ 'open' ] + ", not with " + firstChar )
        
        # Capture any Exception found and dump with current index
        except Exception as ex:
            currIndex = len( self.__originalString ) - len( self.__remainingChars )
            print( "Invalid char at " + str( currIndex ) + ": "+ ex.args[ 0 ] )
            print( self.__originalString )
            print( '^'.rjust( currIndex, ' ' ) )
            
            return structure

        print( "JSON successfully parsed: ", structure )
        return structure


    """
        Method to parse an Object (thus when { was found);
        Note, method can be called Recursively to allow processing nested Objects
    """
    def __parseObject( self  ):
        # Construct object which is represented by JSON Object
        obj = dict()

        while len( self.__remainingChars ) > 0:
            try: # Get next Char, unless the ended only with spaces, then skip to throw correct Exception
                nextChar = self.__getNextChar()
            except:
                continue

            # First check if Object was closed, then return the constructed Object, only if there was no rogue comma before closure
            if nextChar == CHARS[ 'object' ][ 'close' ]:
                if self.__lastWasComma:
                    raise Exception( "Can't close an Object, while separator-comma implied additional attribute" )
                self.__requiresSeparator = False # Reset for next recursive methods

                # Object was correctly closed so return the parsed object
                return obj

            # When Object continues (not closed), first check whether a separator was provided and whether needed
            if nextChar == CHARS[ 'sep' ][ 'attr' ]:
                self.__lastWasComma = True
                if self.__requiresSeparator:
                    self.__requiresSeparator = False
                    continue
                else:
                    raise Exception( "No comma was expected" )

            # Knowing Object is not closed AND no comma was found, check whether an attribute was completed before
            if self.__requiresSeparator:
                raise Exception( "Comma-separator is missing between attributes" )
            self.__lastWasComma = False

            # Attribute parsing
            if nextChar == CHARS[ 'attr' ][ 'open' ]:
                # Parse key and value and assign to object structure
                [ key, value ] = self.__parseAttributeAssignment()
                obj[ key ] = value

            # Invalid character
            else:
                raise Exception( "Unexpected " + nextChar )

        # When no next characters, while object not yet closed
        raise Exception( "JSON ended, but expected Object to be ended" )
        return False


    """
        Method to parse a List (thus when [ was found);
        Note, method can be called Recursively to allow processing nested Objects
    """
    def __parseList( self ):
        # Construct List which is represented by JSON Object
        lst = []

        while len( self.__remainingChars ) > 0:
            try: # Get next Char, unless the ended only with spaces, then skip to throw correct Exception
                nextChar = self.__getNextChar()
            except:
                continue

            # First check if List was closed, then return the constructed List, only if there was no rogue comma before closure
            if nextChar == CHARS[ 'list' ][ 'close' ]:
                if self.__lastWasComma:
                    raise Exception( "Can't close a List, while separator-comma implied additional attribute" )
                self.__requiresSeparator = False # Reset for next recursive methods
                return lst

            # When List continues (not closed), first check whether a separator was provided and whether needed
            if nextChar == CHARS[ 'sep' ][ 'attr' ]:
                self.__lastWasComma = True
                if self.__requiresSeparator:
                    self.__requiresSeparator = False
                    continue
                else:
                    raise Exception( "No comma was expected" )

            # Knowing list is not closed AND no comma was found, check whether an attribute was closed before
            if self.__requiresSeparator:
                raise Exception( "Comma-separator is missing between attributes" )
            self.__lastWasComma = False

            # Value parsing
            lst.append( self.__parseValue( nextChar ) )

        raise Exception( "JSON ended, but expected the Attribute name to be closed with double-quote" )
        return lst

    """
        Method to parse an attribute assignment within an Object: get key, require semi-column and get value
    """
    def __parseAttributeAssignment( self ):
        # Before the opening " was popped before, check [text]": [value]
        attrName = self.__parseString()
        self.__processSemiColumn()
        attrValue = self.__parseValueOfAssignment()
        return [ attrName, attrValue ]

    """
        Method to enforce a semi-column in between an Attribute assignment in an object
    """
    def __processSemiColumn( self ):
        if len( self.__remainingChars ) == 0:
            raise Exception( "JSON ended, but expected ':'" )
        
        nextChar = self.__getNextChar()
        if nextChar != ":":
            raise Exception( "Expected ':' but found " + nextChar )

    """
        Method to parse a value used for an assignment
    """
    def __parseValueOfAssignment( self ):
        while len( self.__remainingChars ) > 0:
            return self.__parseValue( self.__getNextChar() )

        raise Exception( "JSON ended, but expected value assignment completion" )

    """
        Method to process a nextChar and determine which recursive methods to approach
        Both Values in an object-attribute-assignment and Values in Lists have the same allowed data types: String, Number, List and Object
        Therefore this method is centralised to allow shared use
    """
    def __parseValue( self, nextChar ):
        if nextChar == CHARS[ 'attr' ][ 'open' ]:
            val = self.__parseString()

        elif nextChar.isnumeric():
            val = self.__parseNumber( nextChar )

        elif nextChar == CHARS[ 'object' ][ 'open' ]:
            val = self.__parseObject()

        elif nextChar == CHARS[ 'list' ][ 'open' ]:
            val = self.__parseList()

        else:
            raise Exception( "A value is allowed to be a string or numeric value, or a list or object, but found " + nextChar )

        # When Object, List, String or Number was found, require Separator before a next element is parsed
        self.__requiresSeparator = True
        return val

    """
        Method to parse a String value, either used in attribute key or value in an object; or a value in a List
        For efficiency, and since all characters between quotes are allowed, simply check the closing-quote index and continue
        (instead of looping over the remainingChars and popping each)
    """
    def __parseString( self ):
        # Find closing Attribute
        try:
            closingIndex = self.__remainingChars.index( CHARS[ 'attr' ][ 'close' ] )
        except ValueError:
            raise Exception( "No closing-"+ CHARS[ 'attr' ][ 'close' ] + " was found for this text" )

        # Get the String Value (between "") & remove from remainingChars
        stringValue = ''.join( self.__remainingChars[ :closingIndex ] )
        self.__remainingChars = self.__remainingChars[ ( closingIndex + 1 ): ]
        return stringValue

    """
        Method to parse a numeric value
        Since a Number can be both an Integer (only isnumeric characters) or a Float/Decimal (including decimal),
        loop over remainingChars till first character which is not numeric, nor '.'; then combine the strings and convert to Numeric value
        Note, didn't use while .pop() to prevent the next character to already be removed from __remainingChars
        Also constructed numList due to significant better performance of List-manipulations vs String-manipulations
    """
    def __parseNumber( self, firstNum ):
        numList = [ firstNum ]
        isInteger = True
        
        for char in self.__remainingChars:
            if char.isnumeric():
                numList.append( char )
            elif char == CHARS[ 'sep' ][ 'decimal' ]:
                numList.append( char )
                isInteger = False
            else:
                break

        try:
            numberString = ''.join( numList )
            numberValue = int( numberString ) if isInteger else float( numberString )
        except:
            raise Exception( "Invalid number " + ''.join( numList ) )

        # Remove current number from remaining Chars (only after to avoid currentIndex mismatch)
        self.__remainingChars = self.__remainingChars[ len( numList )-1: ]
        return numberValue

    """
        Method to return the first next character which isn't a space, tab or line-break
        Note, no trailing spaces can be left, since input was trimmed to avoid this to happen
    """
    def __getNextChar( self ):
        nextChar = self.__remainingChars.pop( 0 )
        while nextChar.isspace():
            nextChar = self.__remainingChars.pop( 0 )
        return nextChar

"""
    The magic!
"""
# Logic to allow direct validation of Command-line argument jsonString
if len( sys.argv ) == 2: # [ fileReference jsonString ]
    JSONParser( sys.argv[ 1 ] ).parse()
    quit()

# Test scripts:
print( ">> Starting test scripts" )
# Asserting JSON starting character validation
assert dict() == JSONParser( '{}' ).parse(), "Expected valid JSON of empty object"
assert [] == JSONParser( '[]' ).parse(), "Expected valid JSON of empty list"
assert None == JSONParser( '"Naam": "Reinier"' ).parse(), "Should have Parsing exception, since JSON should be list or object"

# Successful complex parsing
inputString = '''{
    "users": [
        {   "Name": "Person1 Surname",
            "LastOrders": [ 350.27, 13, 14.5 ],
            "Details": {
                "LastLogin": "2021-01-07T11:00:00.000Z",
                "Gender": "Unknown"
            }
        },
        {   "Name": "Person2",
            "LastOrders": [],
            "Details": {
                "LastLogin": "Never",
                "Gender": "Neutral"
            }
        }
    ]
}'''
output = JSONParser( inputString ).parse()
assert None != output, "Expected a successfully parsed JSON object"
usersList = output[ "users" ]
assert 2 == len( usersList ), "Expected 2 users to be provided in the output users list"
assert "Person1 Surname" == usersList[ 0 ][ "Name" ], "Expected name of person 1 to be in correct order and still containing space"
assert "Person2" == usersList[ 1 ][ "Name" ], "Expected name of person 2 to be in correct order"
assert 3 == len( usersList[ 0 ][ "LastOrders" ] ), "Expected 3 last Orders for person 1"
assert 0 == len( usersList[ 1 ][ "LastOrders" ] ), "Expected 0 last Orders for person 1"
assert "Neutral" == usersList[ 1 ][ "Details" ][ "Gender" ], "Expected nested Objects to be parsed correctly"

# Validation errors
assert None == JSONParser( '{ "Name": "Reinier" ').parse(), "Missing last closing object-character"
assert None == JSONParser( '{ "Name": "Reinier }').parse(), "Missing closing quote"
assert None == JSONParser( '{ "Age": 30.5.5 }').parse(), "Invalid number"
assert None == JSONParser( '{ "Age": 30, }').parse(), "Rogue comma"
assert None == JSONParser( '{ "Age": 30 "Name": "Reinier" }').parse(), "Missing comma between attributes"

print( ">> All test cases were completed successfully!" )