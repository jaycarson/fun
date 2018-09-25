#!/bin/bash

using_discover(){
    python2 -m unittest discover -p '*Test*.py'
}

using_bash(){
    echo '#!/bin/bash' > test_run.sh
    ls | grep Test >> test_run.sh
    ls | grep Tests >> test_run.sh

    perl -pi -e 's/^/python /' test_run.sh
    perl -pi -e 's/python #!/#!/' test_run.sh

    chmod +x test_run.sh
    ./test_run.sh

    rm test_run.sh
}

using_discover
rm *.pyc
rm ../src/*.pyc
