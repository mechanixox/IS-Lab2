import os

facts = {}
rules = {}

# read file 
def load_file(file_name, data_dict):
    try:
        with open(file_name, "r") as data_file:
            file_contents = data_file.read()
            if file_contents:
                content = file_contents.strip().split('\n')
                data_dict.update({item: True for item in content})
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"\tAn error occurred while reading '{file_name}': {str(e)}")

# save file
def save_file(file_name, data_dict):
    try:
        with open(file_name, "w") as data_file:
            content = "\n".join(data_dict.keys())
            data_file.write(content)
    except Exception as e:
        print(f"\n\tAn error occurred while writing to '{file_name}': {str(e)}")

# print current facts / rules
def print_data(data_dict, data_type):
    print(f"\n\tCurrent {data_type}:")
    for item in data_dict.keys():
        print("\t\t\t\033[93m{}\033[0m".format(item))  


# function to check if a rule has a valid format
def is_valid_rule(rule):
    if rule.startswith("if ") and ", then " in rule:
        conditions, result = rule.split(", then ")
        if conditions.replace("if ", "").strip() == "":
            return False
        condition_facts = conditions.replace("if ", "").split(" and ")
        
        valid_conditions = all(condition.replace(" ", "").isalnum() for condition in condition_facts)
        valid_result = any(char.isalpha() or char.isspace() for char in result)
        
        return valid_conditions and valid_result
    else:
        return False

# add a fact / rule to dictionary
def add_fact_rule(item, data_dict, file_name, data_type):
    if data_type == "rules" and not is_valid_rule(item):
        print(f"\n\t'\033[91m{item}\033[0m' is not a valid rule format. \n\n\tExamples of valid rules: \n\t=> \033[92mif p then q\033[0m \n\t=> \033[92mif x and y then z\033[0m")
        return

    if item not in data_dict:
        data_dict[item] = True
        print(f'\n\t"\033[94m{item}\033[0m" has been added to {data_type}.')
        print("\n")
        print_data(data_dict, data_type)
        save_file(file_name, data_dict)
    else:
        print(f'\n\t"\033[91m{item}\033[0m" already exist in {data_type}.')


# generating new facts
def generate_new_facts(rules_dict, facts_dict):
    new_items = []
    for rule in rules_dict.keys():
        if " then " in rule:
            conditions, result = rule.split(", then ")
            condition_facts = conditions.replace("if ", "").split(" and ")
            if all(condition in facts_dict for condition in condition_facts) and result not in facts_dict:
                new_items.append(result)
        else:
            print(f"\n\tInvalid rule format: {rule}")
           

    if new_items:
        facts_dict.update({item: True for item in new_items})
        print("\n\tNew generated facts:", new_items)
        save_file("facts.txt", facts_dict)  
        generate_new_facts(rules_dict, facts_dict)  # Recursively generate new items
        
        
    else:
        print("\n\t---")

# main loop
while True:
    load_file("facts.txt", facts)
    load_file("rules.txt", rules)
    print("\n")

    print(f"\t\033[94m[1]\033[0m Add a fact")
    print(f"\t\033[94m[2]\033[0m Add a rule")
    print(f"\t\033[94m[3]\033[0m Generate new facts")
    print(f"\t\033[94m[4]\033[0m Display all facts and rules")

    choice = input("\n\tSelect an Option: ")

    if choice == "1":
        while True:
            new_fact = input("\n\tEnter a fact: ").lower()
            os.system('cls')
            if new_fact == '/':
                break
            add_fact_rule(new_fact, facts, "facts.txt", "facts")

    elif choice == "2":
        while True:
            new_rule = input("\n\tEnter a rule: ").lower()
            os.system('cls')
            if new_rule == '/':
                break
            add_fact_rule(new_rule, rules, "rules.txt", "rules")

    elif  choice == "3":
        os.system('cls')
        generate_new_facts(rules, facts)

    elif choice == "4":
        os.system('cls')
        print_data(facts, "facts")
        print_data(rules, "rules")

    elif choice == "5":
        facts = {}
        save_file("facts.txt", facts)
        os.system('cls')
        print(f"\n\tFact(s) deleted.")

    elif choice == "6":
        rules = {}
        save_file("rules.txt", rules)
        os.system('cls')
        print(f"\n\tRule(s) deleted.")

    elif choice == "7":
        facts = {}
        rules = {}
        save_file("facts.txt", facts)
        save_file("rules.txt", rules)
        os.system('cls')
        print(f"\n\t---Added facts and rules deleted---")

    elif choice == "8":
        break

    else:
        os.system('cls')
        print("\n\tInvalid choice. Please try again.")
