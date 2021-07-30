import string
import random
import json


class IdGenerator(object):
    @staticmethod
    def generate_id(length: int=6):
        with open("data/generated_ids.json", "r") as f:
            generated = json.load(f)

        gen = "".join(random.choices(string.ascii_uppercase, k=length))        
        while gen in generated:
            gen = ''.join(random.choices(string.ascii_uppercase, k=length))

        generated.append(gen)
        
        with open("data/generated_ids.json", "w") as f:
            json.dump(generated, f, indent=4)
            
        return gen
