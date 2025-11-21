import os

def printTerminal(text:str, mode:str="recv", title:str|None=None):
    '''
        formating text to the console for a better look and feel.
        titled --> for printing errors and headings
        else:
            modes:
                recv --> printing received text
                sent --> printing sent text
    '''
    terminal_length = os.get_terminal_size().columns
    format_ratio = 0.7
    formated_text = ""

    if len(text) == 0:
        return
    
    if title is not None:
        
        title = f" <{title}> "
        x = (terminal_length - len(title))//2
        formated_text += f"{'-'*x}{title}{'-'*x}"

        y = (terminal_length - len(text))//2
        formated_text += f"\n{' '*y}{text}"

        formated_text += f"\n{'-'*terminal_length}"

    else:
        words = text.split()
        x = int(terminal_length*format_ratio) + 3

        if len(text) + 2 < x:
            x = len(text) + 4
            padding_left = terminal_length - (x + 2)
            if mode == "recv":
                formated_text += f"@{'-'*x}+\n"
                formated_text += f"| {text}{' '*(x-len(text)-1)}|\n"
                formated_text += f"+{'-'*x}+\n"

            else:
                formated_text += f"{' '*padding_left}@{'-'*x}+\n"
                formated_text += f"{' '*padding_left}| {text}{' '*(x-len(text)-1)}|\n"
                formated_text += f"{' '*padding_left}+{'-'*x}+\n"

        else:
            padding_left = int(terminal_length*(1-format_ratio)) - 4

            if mode == "recv":
                formated_text += f"@{'-'*x}+\n"

                line = f"| {words[0]}"
                for word in words[1:]:
                    word = f" {word}"
                    if len(line + word) + 2 < x:
                        line += word

                    else:
                        formated_text += f"{line} {' '*(x-len(line))}|\n"
                        line = f"|{word}"

                formated_text += f"{line} {' '*(x-len(line))}|\n"
                formated_text += f"+{'-'*x}+\n"

            else:
                formated_text += f"{' '*padding_left}+{'-'*x}@\n"

                line = f"| {words[0]}"
                for word in words[1:]:
                    word = f" {word}"
                    if len(line + word) + 2 < x:
                        line += word

                    else:
                        formated_text += f"{' '*padding_left}{line} {' '*(x-len(line))}|\n"
                        line = f"|{word}"

                formated_text += f"{' '*padding_left}{line} {' '*(x-len(line))}|\n"
                formated_text += f"{' '*padding_left}+{'-'*x}+\n"

    print(formated_text)


text = "Reading is easier, too, in the new Reading view. You can collapse parts of the document and focus on the text you want. If you need to stop reading before you reach the end, Word remembers where you left off - even on another device."

printTerminal(text, mode="recv")
printTerminal("text hello", mode="sent")