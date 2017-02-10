### Usage

#### Python

Built on Python 2.7 on MacOS

```
$ python parallelism_python.py
```

#### Golang

Built on Go 1.75 on MacOS

```
$ go run paralleism_go.go
```

#### Ruby

Built on Ruby 2.3.1 on MacOS. Process forking will only work on *nix systems

```
$ ruby parallelism_ruby.rb
```

### Elixir 

Built on OTP 19, Elixir 1.4.1 (the necessary async_stream function does not exist on Elixir) on MacOS

```
$ elixir -r parallelism_elixir.ex -e 'Concurrency.async_with_limit'
$ elixir -r parallelism_elixir.ex -e 'Concurrency.async_eager
$ elixir -r parallelism_elixir.ex -e 'Concurrency.async_lazy'
$ elixir -r parallelism_elixir.ex -e 'Concurrency.sync'
```

