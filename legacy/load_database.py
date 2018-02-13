# Pablo Abad 2017
#
# Main program to update the tosh
import argparse
from legacy.database import ToshlDatabase

def read_token(token_file):
    with open(token_file, 'r') as f:
        token = f.read().strip()
    return token

def save_categories(categories_file, database):
    categories_names = database.getCategories()
    categories = []
    for categoryName in categories_names:
        category_id = database._getCategoryId(categoryName)
        categories.append((category_id, categoryName))
    categories.sort(key=lambda x: x[0])
    with open(categories_file, 'w') as f:
        f.writelines(map(lambda c: c[0].encode("UTF-8") + '\t' + c[1].encode("UTF-8")+ '\n', categories))

def save_tags(tags_file, database):
    tag_names = database.getTags()
    tags = []
    for tag_name in tag_names:
        tag_id = database._getTagId(tag_name)
        tags.append((tag_id, tag_name))
        tags.sort(key=lambda x: x[0])
    with open(tags_file, 'w') as f:
        f.writelines(map(lambda c: c[0].encode("UTF-8") + '\t' + c[1].encode("UTF-8")+ '\n', tags))

def save_accounts(accounts_file, database):
    account_names = database.getAccounts()
    accounts = []
    for account_name in account_names:
        account_id = database._getAccountId(account_name)
        accounts.append((account_id, account_name))
        accounts.sort(key=lambda x: x[0])
    with open(accounts_file, 'w') as f:
        f.writelines(map(lambda c: c[0].encode("UTF-8") + '\t' + c[1].encode("UTF-8")+ '\n', accounts))

def run(token_file, suffix):
    token = read_token(token_file)
    database = ToshlDatabase(token)
    save_categories('data/Categories_'+ suffix +'.csv', database)
    save_tags('data/Tags_'+ suffix +'.csv', database)
    save_accounts('data/Accounts_' + suffix + '.csv', database)


def main():
    parser = argparse.ArgumentParser(prog="load_database",
                                     description='Synchronizes the Toshl account to a CSV transfers file')
    parser.add_argument('token_file')
    parser.add_argument('suffix')
    args = parser.parse_args()
    run(args.token_file, args.suffix)


if __name__ == "__main__":
    main()
