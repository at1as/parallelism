defmodule Concurrency do
  alias Concurrency


  def slow_operation(id) do
    # Prints input args, process ID, and sleeps 4 seconds
    IO.puts("id#{id} : Started (process id " <> "#{:erlang.pid_to_list(self())}" <> ")")
    :timer.sleep(4000)
    IO.puts("id#{id} : Finished (process id " <> "#{:erlang.pid_to_list(self())}" <> ")")
    id
  end

  def async_eager do
    # Runs all tasks immediately (Enum.map is eager)
    (1..10)
    |> Enum.map(&Task.async(Concurrency, :slow_operation, [&1]))
    |> Enum.map(&Task.await(&1))
  end
  
  def async_lazy do
    # Runs tasks sequentially (Stream.map is lazy)
    (1..10)
     |> Stream.map(&Task.async(Concurrency, :slow_operation, [&1]))
     |> Enum.map(&Task.await(&1))
  end

  def sync do
    # Runs tasks sequentially
    (1..10)
    |> Enum.map(fn(x) -> slow_operation(x) end)
  end

  def async_with_limit do
    # Runs tasks asynchronously, with a set concurrency limit 
    cores = System.schedulers_online
    IO.puts "Starting with max concurrency #{cores}"

    (1..17)
    |> Task.async_stream(Concurrency, :slow_operation, [], max_concurrency: cores)
    |> Enum.map(fn {:ok, id} -> id end)
  end


end

