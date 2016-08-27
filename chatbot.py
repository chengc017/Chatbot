# -*- coding: utf-8 -*-

import console
import medicine.medicine as medicine

def main():
    chatbot = Chatbot()
    chatbot.waiting_loop()

class Chatbot(object):

    def __init__(self, name="NCKU"):
        self.name = name             # The name of chatbot.

        self.speech = ''             # The lastest user's input
        self.speech_domain = ''      # The domain of speech.
        self.speech_matchee = ''     # The matchee term of speech.
        self.speech_path = None      # The classification tree traveling path of speech.
        self.assigneer = None         # The module will handle user's intend.

        self.domain_similarity = 0.0 # The similarity between domain and speech.

        self.console = console.Console(model_path="model/ch-corpus-3sg.bin")

    def waiting_loop(self):

        while True:

            speech = input("Hi, I'm " + self.name + '\n')
            self.rule_match(speech) # to find the most similar domain with speech.
            self.set_assigner() # set a module to handle user's task.
            result = self.module_switch()

            if result is None:
                print(self.get_response())
            else:
                print(result)


    def rule_match(self, speech):

        """
        Get the rule has best similarity with user's input,
        and set domain,path,similarity based on that rule.
        """

        res,self.last_path = self.console.rule_match(speech, best_only=True)
        self.speech = speech
        self.domain_similarity,self.speech_domain,self.speech_matchee = res

    def get_response(self):
        """
        Generate a response to user's speech.
        Please note that this response is pre-defined in the json file,
        not the result return by sub_module.
        """
        response = self.console.get_response(self.speech_domain)
        if response is None:
            return "I know you are talking about '%s', but I don't know how to response." % self.speech_domain
        else:
            return response

    def set_assigner(self):

        """
        Extract the root rule in result.
        """
        if self.last_path == "":
            self.assigner = self.speech_domain
        else:
            self.assigner = self.last_path.split('>')[0]

    def module_switch(self):

        if self.assigner == "病症":
            #Enter the medical module.
            listener = medicine.MedicalListener(self.console)
            if listener.look_up(self.speech_domain):
                status, response = listener.processing_baseline(self.speech,[])
                print(status)
                return response
            else:
                return None
        else:
            return None


if __name__ == '__main__':
    main()
