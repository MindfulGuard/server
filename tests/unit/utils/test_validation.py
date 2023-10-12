from mindfulguard.utils import Validation

class Validations:
    def __init__(self):
        self.__validation = Validation()
    
    def is_login(self):
        valid:bool = self.__validation.validate_login("MyLogin432-_")
        not_valid:bool = self.__validation.validate_login(
            "MyLogin432-%$)98485345b347n5b3894&(*NB($&%BN(*%B<V<$V%$<V_"
            )
        return (valid,not_valid)
    
    def is_secret_string(self):
        valid:bool = self.__validation.validate_secret_string(
            "5tt7Cq8nMnyZUaMlX178Ro6FQD1lAN0fuhRo2MLtvjpU39wrjK2yt9K4szT4qH9Y"
            )
        not_valid:bool = self.__validation.validate_secret_string(
            "b54398b57n349v759834m7"
            )
        return (valid,not_valid)
    
    def is_token(self):
        valid:bool = self.__validation.validate_token(
            "Wba8AeNpzUh0jEl3r7gi3V65ZaWq9d39MwWLH8dTLmtUdxreYpH5IFIf6fTcFzVk9yN9plLaDMAR42bGervCAUy1g8OJy9b6s1W2iYRmHg6RDGHgXakg3BlHdsRWy1Bl"
            )
        not_valid:bool = self.__validation.validate_token(
            "b5437b49387n8v783m9v5"
            )
        return (valid,not_valid)
    
    def is_uuid(self):
        valid:bool = self.__validation.validate_is_uuid("e9e09ac1-4e9e-4049-b1a1-192c786aef30")
        not_valid:bool = self.__validation.validate_is_uuid("5-55-4b45-b-b")
        return (valid,not_valid)
    
    def validate_description(self):
        valid:bool = self.__validation.validate_description("""
        Has exposed far. 
        Over game disposing viewing me age smiling position agreeable. Very nothing exertion decisively barton one solid colonel year told chamber smart dwelling introduced. Peculiar assure collecting linen china. Truth unsatiable joy appetite possible direct unpleasing each. Otherwise difficult relied pleasant preferred rich right reserved large sufficient weeks these letter sensible. 
        Ham warmly looked general eldest replying never scale. Indulged ignorant whether sportsman daughters admiration show. Perfectly visitor opinions may blessing unpleasing that better fruit household explained offer need his. Suspicion giving out suitable whose ﻿no devonshire mind behind. Domestic made necessary how shewing high. 
        In mirth noise need manners down wonder shameless view purse detract. Call cordially speedily letter advantages some first from likewise summer. Started misery with books remarkably name. Servants tended away pianoforte received moments enough dwelling arranging prepared after. Viewing sense convinced hung concealed maids extended comparison agreed society soon none just marriage wise misery bringing. 
        """)

        not_valid:bool = self.__validation.validate_description("""
        Learning own met bachelor rapturous than considered windows tedious bore like resolution arrived ferrars feebly good. 
        Valley be introduced difficult things. Amounted viewing affection put admitting introduced men beyond. Court resolving hold marry mother result performed roused unwilling know fanny pianoforte plate new enough. Children cordial welcome set by who mother hung vexed regular. Staying warrant none doors brother pursuit immediate cousin pain shameless. 
        Began distant wound. Do better know branched voice day goodness heard improved. Any waited since direct breeding diminution excellent mistaken horrible songs future parlors examine. Introduced mistaken marianne alteration horrible lasting newspaper graceful do into. Subjects all difficult or. 
        Sense so preference differed suffer alone fat. Chief hills outweigh offence. Hand dine produced friendship into answer besides hope. Felicity order eagerness sitting contented attempted tried respect share our. Formerly announcing eldest they some eyes. 
        Solicitude friendly matter denoting entered screened suppose all case celebrated use none. Provided forbade household rest view before pure times sooner visit blessing. Delivered expect sixteen smallness elinor resources oppose several ignorant. Forming property account placing cottage children smile feelings believed  certainly five bore winding. Absolute discovery horrible too attention assistance call greater edward times morning. 
        Formed cheered period speaking are solicitude means cottage fine worth size party course theirs. The continue those fat colonel consulted except nay every gone started prospect motionless differed daughter. Hardly whose seems maids hundred general get carriage others suppose consisted length men. Know estate viewing their arrival. 
        """)
        return (valid,not_valid)

    def is_TOTP_code(self):
        valid:bool = self.__validation.validate_TOTP_code("583063")
        not_valid:bool = self.__validation.validate_TOTP_code("C8F0335")
        return (valid,not_valid)
    
    def is_user_agent(self):
        valid:bool = self.__validation.validate_user_agent("""
        Has exposed far. 
        Over game disposing viewing me age smiling position agreeable. Very nothing exertion decisively barton one solid colonel year told chamber smart dwelling introduced. Peculiar assure collecting linen china. Truth unsatiable joy appetite possible direct unpleasing each. Otherwise difficult relied pleasant preferred rich right reserved large sufficient weeks these letter sensible. 
        Ham warmly looked general eldest replying never scale. Indulged ignorant whether sportsman daughters admiration show. Perfectly visitor opinions may blessing unpleasing that better fruit household explained offer need his. Suspicion giving out suitable whose ﻿no devonshire mind behind. Domestic made necessary how shewing high. 
        In mirth noise need manners down wonder shameless view purse detract. Call cordially speedily letter advantages some first from likewise summer. Started misery with books remarkably name. Servants tended away pianoforte received moments enough dwelling arranging prepared after. Viewing sense convinced hung concealed maids extended comparison agreed society soon none just marriage wise misery bringing. 
        """)

        not_valid:bool = self.__validation.validate_user_agent("""
        Learning own met bachelor rapturous than considered windows tedious bore like resolution arrived ferrars feebly good. 
        Valley be introduced difficult things. Amounted viewing affection put admitting introduced men beyond. Court resolving hold marry mother result performed roused unwilling know fanny pianoforte plate new enough. Children cordial welcome set by who mother hung vexed regular. Staying warrant none doors brother pursuit immediate cousin pain shameless. 
        Began distant wound. Do better know branched voice day goodness heard improved. Any waited since direct breeding diminution excellent mistaken horrible songs future parlors examine. Introduced mistaken marianne alteration horrible lasting newspaper graceful do into. Subjects all difficult or. 
        Sense so preference differed suffer alone fat. Chief hills outweigh offence. Hand dine produced friendship into answer besides hope. Felicity order eagerness sitting contented attempted tried respect share our. Formerly announcing eldest they some eyes. 
        Solicitude friendly matter denoting entered screened suppose all case celebrated use none. Provided forbade household rest view before pure times sooner visit blessing. Delivered expect sixteen smallness elinor resources oppose several ignorant. Forming property account placing cottage children smile feelings believed  certainly five bore winding. Absolute discovery horrible too attention assistance call greater edward times morning. 
        Formed cheered period speaking are solicitude means cottage fine worth size party course theirs. The continue those fat colonel consulted except nay every gone started prospect motionless differed daughter. Hardly whose seems maids hundred general get carriage others suppose consisted length men. Know estate viewing their arrival.
        Has exposed far. 
        Over game disposing viewing me age smiling position agreeable. Very nothing exertion decisively barton one solid colonel year told chamber smart dwelling introduced. Peculiar assure collecting linen china. Truth unsatiable joy appetite possible direct unpleasing each. Otherwise difficult relied pleasant preferred rich right reserved large sufficient weeks these letter sensible. 
        Ham warmly looked general eldest replying never scale. Indulged ignorant whether sportsman daughters admiration show. Perfectly visitor opinions may blessing unpleasing that better fruit household explained offer need his. Suspicion giving out suitable whose ﻿no devonshire mind behind. Domestic made necessary how shewing high. 
        In mirth noise need manners down wonder shameless view purse detract. Call cordially speedily letter advantages some first from likewise summer. Started misery with books remarkably name. Servants tended away pianoforte received moments enough dwelling arranging prepared after. Viewing sense convinced hung concealed maids extended comparison agreed society soon none just marriage wise misery bringing.  
        """)
        return (valid,not_valid)
    
    def is_json(self):
        valid:bool = self.__validation.validate_json("{'key1':'value1','key2':'value2'}")
        not_valid:bool = self.__validation.validate_json("{'key1':'value1','key1':'value2',[4,5,5,6,3,6,3]}")
        return (valid,not_valid)


def test_validations():
    obj = Validations()

    __is_login = obj.is_login()
    __is_login_valid = __is_login[0]
    __is_login_not_valid = __is_login[1]

    __is_secret_string = obj.is_secret_string()
    __is_secret_string_valid = __is_secret_string[0]
    __is_secret_string_not_valid = __is_secret_string[1]

    __is_token = obj.is_token()
    __is_token_valid = __is_token[0]
    __is_token_not_valid = __is_token[1]

    __is_uuid = obj.is_uuid()
    __is_uuid_valid = __is_uuid[0]
    __is_uuid_not_valid = __is_uuid[1]

    __validate_description = obj.validate_description()
    __validate_description_valid = __validate_description[0]
    __validate_description_not_valid = __validate_description[1]

    __is_TOTP_code = obj.is_TOTP_code()
    __is_TOTP_code_valid = __is_TOTP_code[0]
    __is_TOTP_code_not_valid = __is_TOTP_code[1]

    __is_is_user_agent = obj.is_user_agent()
    __is_is_user_agent_valid = __is_is_user_agent[0]
    __is_is_user_agent_not_valid = __is_is_user_agent[1]

    __is_json = obj.is_json()
    __is_json_valid = __is_json[0]
    __is_json_not_valid = __is_json[1]

    assert __is_login_valid == True
    assert __is_login_not_valid == False

    assert __is_secret_string_valid == True
    assert __is_secret_string_not_valid == False

    assert __is_token_valid == True
    assert __is_token_not_valid == False

    assert __is_uuid_valid == True
    assert __is_uuid_not_valid == False

    assert __validate_description_valid == True
    assert __validate_description_not_valid == False

    assert __is_TOTP_code_valid == True
    assert __is_TOTP_code_not_valid == False

    assert __is_is_user_agent_valid == True
    assert __is_is_user_agent_not_valid == False

    assert __is_json_valid == True
    assert __is_json_not_valid == False