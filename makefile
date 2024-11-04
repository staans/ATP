files := $(wildcard cpp/*)

.PHONY: clean

python/cpp_lib.so: $(files)
	g++ -fPIC -Og -shared $(files) -o $@

clean:
	rm python/cpp_lib.so