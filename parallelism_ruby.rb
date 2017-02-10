require 'time'

def long_duration(id)
  puts "Starting id #{id} with pid #{$$}"
  sleep 4
  puts "Finished id #{id} with pid #{$$}"
end


def synchronous
  start = Time.now
  puts "Starting iterative solution"

  (0..10).each do |num|
    long_duration(num)
  end

  stop = Time.now
  puts "Finishing iterative solution.\nRuntime #{stop - start}"
end


def threaded
  start = Time.now
  puts "Starting threaded solution"

  threads = []
  (0..10).each do |num|
    threads << Thread.new { long_duration(num) }
  end

  threads.map(&:join)

  stop = Time.now
  puts "Finishing threaded solution.\nRuntime #{stop - start}"
end


def processes
  start = Time.now
  puts "Starting multiprocess solution"

  processes = []
  (0..10).each do |num|
    processes << fork { long_duration(num) }
  end

  while true
    process_runing = false
    processes.each do |process_num|
      begin
        Process.getpgid(process_num) # Throws exception unless process is still active
        process_running = true
      rescue Errno::ESRCH
      end
    end

    break unless process_running
  end

  stop = Time.now
  puts "Finishing process solution.\nRuntime #{stop - start}"
end


puts "Iterative Solution launched from process id #{$$}"
synchronous()

puts "Threaded Solution launched from process id #{$$}"
threaded()

puts "Multi-Process Solution lauched from process id #{$$}"
processes()

