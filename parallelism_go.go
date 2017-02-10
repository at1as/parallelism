package main

import (
  "fmt"
  "time"
  "sync"
  )


var wg sync.WaitGroup

//func sleeper(id int) {
//  fmt.Printf("Starting function for process %d\n", id)
//  time.Sleep(4 * time.Second)
//  fmt.Printf("Completed function for process %d\n", id)
//}

func sleeper(id int, waitgroup bool) {
  if waitgroup {
    defer wg.Done()
  }
  fmt.Printf("Starting function for process %d\n", id)
  time.Sleep(4 * time.Second)
  fmt.Printf("Completed function for process %d\n", id)
}

func synchronous() {
  for i := 0 ; i < 10 ; i++ {
    sleeper(i, false)
  }
}


func async() {
  for i := 0 ; i < 10 ; i++ {
      wg.Add(1)
      go sleeper(i, true)
  }
  wg.Wait()
}

func main() {
  start := time.Now()
  fmt.Println("\nStarting Synchronous Solution... \n")
  synchronous()
  done := time.Now()
  fmt.Printf("\nDone Synchronous solution in %+v\n", done.Sub(start))
  
  start = time.Now()
  fmt.Println("\nStarting Async Solution...")
  async()
  done = time.Now()
  fmt.Printf("\nDone Async Solution... %+v\n", done.Sub(start))
}

