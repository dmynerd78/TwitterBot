import time


def colorPrint(message, color=91):
    """ Print out colored text """

    global coloredText

    if coloredText:
        return ("\033[%sm%s\033[0m" % (color, message))
    else:
        return (message)


# TODO Convert everything to log
def log(message, level="info"):
    """ Levels: CRITICAL, ERROR, WARNING, INFO, DEBUG """

    config_level = config["log_level"]
    level.upper()
    level_template = {
        "CRITICAL": {"level": 1, "color": "1;41"},
        "ERROR": {"level": 2, "color": "1;91"},
        "WARNING": {"level": 3, "color": "1;93"},
        "INFO": {"level": 4, "color": "1;95"},
        "DEBUG": {"level": 5, "color": "1;96"}
    }

    try:
        level_template[level]
    except:
        level = "INFO"

    if level_template[level]["level"] >= level_template[config_level]["level"]:
            print("{} [{}] {}".format(
                time.strftime("[%I:%M:%S %p]"),
                level.upper(),
                colorPrint(message, level_template[level]["color"]))
            )
    else:
        pass
        # log("Level not high enough for message '{}' Level: {}".format(message, level), "WARNING")

if __name__ == "__main__":
    from auth import config_read

    global coloredText
    global configLevel

    coloredText = True
    configLevel = config_read()["log_level"]
    log("Test Log thjingoaismdoijasidasd", configLevel)

    # for i in range(0,100):
    #     print("\033[%sm%s\033[0m" % (i, i))
    # colorPrint("This should be Bold (1) with a cyan background (46)", "1;46")
