export JSON_JAVA:=/usr/share/java
export CLASSPATH:=$(CLASSPATH):$(JSON_JAVA)/json-simple.jar

all: Generate.class ../codepoints.json
	java Generate ../codepoints.json ../../databases/

clean:
	rm *.class

Generate.class: Generate.java
	javac Generate.java
