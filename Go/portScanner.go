package main

import (
	"fmt"
	"net"
	"sort"
)

func worker(addr string, ports chan int, results chan int) {
	for p := range ports {
		fmt.Printf("Scanning %d...\n", p)
		address := fmt.Sprintf("%s:%d", addr, p)

		conn, err := net.Dial("tcp", address)
		if err != nil {
			results <- 0
			continue
		}

		conn.Close()
		results <- p
	}
}

func scanPorts(addr string, nrPorts int, goRoutines int) {
	var openPorts []int
	ports := make(chan int, goRoutines)
	results := make(chan int)

	for i := 0; i < cap(ports); i++ {
		go worker(addr, ports, results)
	}

	go func() {
		for i := 1; i <= nrPorts; i++ {
			ports <- i
		}
	}()

	for i := 1; i <= nrPorts; i++ {
		port := <-results
		if port != 0 {
			openPorts = append(openPorts, port)
		}
	}

	close(results)
	close(ports)

	sort.Ints(openPorts)
	fmt.Printf("=== Results for %s ===\n", addr)
	for _, p := range openPorts {
		fmt.Printf("%d open\n", p)
	}
}

func main() {
	scanPorts("scanme.nmap.org", 1024, 1000)
}
