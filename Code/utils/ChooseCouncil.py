from .GetVatican1Documents import *
from .GetVatican2Documents import *

### Get Vatican Documents ###
def ChooseCouncilFunction(council, LanguageCode):
    if council.upper() == 'I':
        return GetVatican1Documents(LanguageCode)
    elif council.upper() == 'II':
        return GetVatican2Documents(LanguageCode)
    else:
        raise ValueError("Council must be either 'I' or 'II'")