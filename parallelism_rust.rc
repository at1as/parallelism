use std::{thread, time};
use std::time::SystemTime;

fn sleeper(i: i32) {
  println!("Starting loop : {}", i);
  thread::sleep(time::Duration::from_millis(4000));
  println!("Finished loop : {}", i);
}


fn synchronous() {
  for x in 0..10 {
    sleeper(x);
  }
}

fn asynchronous() {
  
  let mut threads = Vec::new();
  for x in 0..10 {
    threads.push(
      thread::spawn(move || {
        sleeper(x);
      })
    );
  }

  for t in threads {
    t.join().unwrap();
  }
}


fn main(){
  let now_async = SystemTime::now();
  println!("\nParallel Solution : \n");
  asynchronous();

  match now_async.elapsed() {
    Ok(elapsed) => { println!("\nCompleted in {:?}s", ((elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1000_000_000.0))) }
    Err(_) => { println!("Error.") }
  };
  

  let now_sync = SystemTime::now();
  println!("\nSynchronous Solution : \n");
  synchronous();

  match now_sync.elapsed() {
    Ok(elapsed) => { println!("\nCompleted in {:?}s", ((elapsed.as_secs() as f64) + (elapsed.subsec_nanos() as f64 / 1000_000_000.0))) }
    Err(_)      => { println!("Error") }
  };
}
