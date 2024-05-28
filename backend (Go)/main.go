// main.go

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

// Response represents the structure of the API response
type Response struct {
	Query   string   `json:"query"`
	Results []string `json:"results"`
}

func main() {
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/search", searchHandler)

	fmt.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Go backend!")
}

func searchHandler(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")

	// Replace this with your actual search logic
	results := search(query)

	response := Response{
		Query:   query,
		Results: results,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// Dummy search function
func search(query string) []string {
	// Dummy search logic
	return []string{"Result 1", "Result 2", "Result 3"}
}
