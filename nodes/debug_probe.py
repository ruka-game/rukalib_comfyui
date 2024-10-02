# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_typ = AnyType("*")

class RukaDebugProbe:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (any_typ,)
            },
        }

    RETURN_TYPES = (any_typ,)
    FUNCTION = "process"

    CATEGORY = "utils"

    def process(
        self,
        any
    ):
        print(any)
        return (any,)