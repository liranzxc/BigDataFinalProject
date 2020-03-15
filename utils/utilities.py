class Utilities:
    @staticmethod
    def clean_word(word, allow_numbers=False):
        cleaned = ""
        numbers = '0123456789'
        not_allowed = '!,.?":;@#$%^&*()=+-\\'
        if allow_numbers:
            not_allowed += numbers

        for char in word:
            if char in not_allowed:
                char = ""
            cleaned += char
        return cleaned

    @staticmethod
    def clean_sentence(sentence, allow_numbers=False):
        words1 = []
        words2 = sentence.split()
        for word in words2:
            word = Utilities.clean_word(word, allow_numbers)
            words1.append(word)
        return words1
