from log.log import *

class ConfigFile():
    """ Creates a configuration file with given path and key vaule pairs.
        If the file does not exist it will be created using the default values.

        An example of an initialization could be:

        conf = ConfigFile(
            "mysense/resources/test.conf",
            (
                ("enabled", "true", "this is an example boolean\nsecond line", bool),
                ("number", "42", "this is an example number", uint),
                ("str", "hello world", "this is an example string", string)
            )
        )
    """
    def __init__(self, path, values):
        self.path = path

        # create map with default values
        self.dict = {}
        for v in values:
            # gather key, value and type
            key = v[0]
            value = v[1]
            type = v[3]

            # cast string value
            casted = self.__cast(value, type)
            if casted == None:
                log_warning("Type of config variable '" + key + "' is '" + type + "' but given value '" + value + "' is invalid.")
            else:
                self.dict[key] = casted

        # try to open config file
        try:
            log_debug("Reading config file '" + self.path + "'.")
            f = open(path, "r")

            # parse config file line by line
            line = f.readline()
            count = 1

            while line:
                pair = self.__parse_line(line, count)
                if pair != None:

                    found = False
                    for v in values:
                        if pair[0] == v[0]:
                            found = True
                            value = self.__cast(pair[1], v[3])

                            if value == None:
                                __parse_error(count, "invalid " + str(v[3]) + " '" + pair[1] + "'")
                            else:
                                self.dict[pair[0]] = value

                    if not found:
                        __parse_error(count, "invalid variable '" + pair[0] + "'")


                line = f.readline()
                count += 1

        # if file does not exist create it
        except:
            log_debug("Config file '" + path + "' not found.")

            # try to create config file
            try:
                f = open(path, "w")

                for v in values:
                    # write description as comment
                    for l in str(v[2]).split("\n"):
                        f.write("# " + l + "\n")

                    # add default configuration as comment2
                    f.write("#\n# " + v[0] + " = \"" + v[1] + "\"\n")

                    # write key and standart value
                    f.write(v[0] + " = \"" + v[1] + "\"\n\n") # TODO: remove whitespaces (this was just for testing)

                log_info("Created config file '" + path + "'.")

            # failed to create config file
            except Exception as e:
                log_warning("Could not create config file '" + path + "': " + str(e) + ".")

    def __parse_error(self, line_nr, message):
        log_warning("Invalid line " + str(line_nr) + " ignored in file '" + self.path + "': " + message + ".")


    def __parse_line(self, line, line_nr):
        # parsing state
        state = 0

        # key and value to be returned
        key = ""
        value = ""

        # parse line character by character
        for c in line:

            # start - skip whitespaces and detect comments
            if state == 0:

                # skip whitespaces
                if c == " " or c == "\t" or c == "\n":
                    continue

                # detect comment
                elif c == "#":
                    return None

                # start of key
                else:
                    key += c
                    state += 1

            # get key
            elif state == 1:

                # stop if whitespace is found
                if c == " " or c == "\t":
                    state += 1

                # if equals is found continue with value
                elif c == "=":
                    state += 2

                # continue with key
                else:
                    key += c

            # equal sign
            elif state == 2:

                # skip whitespaces
                if c == " " or c == "\t":
                    continue

                # if equals is found continue with value
                elif c == "=":
                    state += 1

                # invalid line
                else:
                    self.__parse_error(line_nr, "expected equals after variable name")
                    return None

            # start of value is marked by quotation marks
            elif state == 3:

                # skip whitespaces
                if c == " " or c == "\t":
                    continue

                # if quotation mark start with value
                elif c == "\"":
                    state += 1

                # invalid line
                else:
                    self.__parse_error(line_nr, "expected quotation mark after equals")
                    return None

            # get value
            elif state == 4:

                # end of value is marked by quotation mark
                if c == "\"":
                    state += 1

                else:
                    value += c

            # end of key/value definition reached, only accept whitespaces and comments now
            elif state == 5:

                # skip whitespaces
                if c == " " or c == "\t" or c == "\n":
                    pass

                # comment
                elif c == "#":
                    pass

                # invalid line
                else:
                    self.__parse_error(line_nr, "expected line end or comment after declaration")
                    return None

        if state == 0:
            return None

        elif state != 5:
            self.__parse_error(line_nr, "unexpected end of line.")
            return None

        # finally we have a valid line with a key/value pair
        return (key, value)

    def __cast(self, value, type):
        # string type
        if type == ConfigFile.VariableType.string:
            return value

        # bool type
        elif type == ConfigFile.VariableType.bool:
            if value == "1" or value.lower() == "true":
                return True
            elif value == "0" or value.lower() == "false":
                return False
            else:
                return None

        # uint type
        elif type == ConfigFile.VariableType.uint:
            try:
                nr = int(value)
                if nr < 0:
                    return None
                return nr
            except:
                return None

        return None

    def get(self, key):
        # check if requested variable is available
        if key not in self.dict:
            log_warning("Variable '" + key + "' not found in config file '" + self.path + ".")
            return None

        # get value from dictionary
        return self.dict[key]

    class VariableType():
        bool = "bool"
        uint = "uint"
        string = "string"
