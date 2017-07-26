import sys
from myapp import create_app
from instance import environments

err_string = """\n\tOption not provided
        Enter: 'python run.py -h' or 'python run.py --help'
        to get list of available options
        """

try:
    if sys.argv[1] and sys.argv[1] in environments:
        app = create_app(environments.get(sys.argv[1]))
        app.run()

    elif sys.argv[1] and sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print ('\n\nUsage:')
        print ('\t"python run.py <environment>"')
        print ('\t\tEnvironment Options:\n\t\t\t development \n\t\t\t production')
        print ('Testing:')
        print ('\t"python test.py"\n\n')

    else:
        print (err_string)

except IndexError:
    print (err_string)

exit()