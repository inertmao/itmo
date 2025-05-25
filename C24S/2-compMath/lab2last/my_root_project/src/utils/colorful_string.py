
# ========== Utils ==========

class ColorfulString:
    ANSI_RESET = "\u001B[0m"
    ANSI_CYAN = "\u001B[36m"

    @staticmethod
    def println(msg: str):
        print(f"{ColorfulString.ANSI_CYAN}{msg}{ColorfulString.ANSI_RESET}")
