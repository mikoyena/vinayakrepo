#decorator function to extract domain and subdomian from an email address.

def extract_subdomain(func):
    def wrapper_function(value):
        print("I am extract_subdomain")
        address = func(value)
        index_of_at_the_rate = address.rfind('@')
        index_of_dot = address.rfind('.')
        return address[index_of_at_the_rate + 1:index_of_dot]

    # return func(value)
    return wrapper_function


def extract_domain(func):
    def wrapper_function(value):
        print("I am extract_domain")
        address = func(value)
        index_of_dot = address.rfind('.')
        print(address[index_of_dot + 1:])
        return address

    return wrapper_function


@extract_subdomain
@extract_domain
def get_input_email(email):
    return email


output = get_input_email("vinuparab1840@mymailbox.yahoo.in")

print(output)
