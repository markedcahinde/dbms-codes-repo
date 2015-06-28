import sys

def add(x,y):
	return x+y

def main():
	if len(sys.argv) >= 2:
		name = sys.argv[1] + ' ' + sys.argv[2]
	else:
		name = 'World'
	print 'hello', name

if __name__ == '__main__':
	main()
