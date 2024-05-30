package main

import (
    "net/http"

    "github.com/gin-gonic/gin"
	//"time"
)

func main() {
	r := gin.Default()
	// define the routes
	r.POST("/auth", authenticator)
	r.Run(":5000")

 }

 func comapre_string(a string, b string) bool {
	 //compare sizes 
	 if len(a) != len(b) {
		 return false
	 }
	 //compare each character
	 for i := 0; i < len(a); i++ {
		 if a[i] != b[i] {
			 return false
		 }
	 }
	 return true
 }



type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
}
 func authenticator(c *gin.Context) {
	
	var user User
	if err := c.ShouldBindJSON(&user); err != nil {
	   c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	   return
	}
	if comapre_string(user.Username, "admin") && comapre_string(user.Password, "ping20241337leet2137") {
	   c.JSON(http.StatusOK, gin.H{"message": "success"})
	} else {
	   c.JSON(http.StatusUnauthorized, gin.H{"message": "unauth"})
	}

}