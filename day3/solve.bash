cat input | sed -e 's/mul/\nmul/g' -e 's/)/)\n/g' | grep 'mul([0-9][0-9]*,[0-9][0-9]*)' | ./mul_add
