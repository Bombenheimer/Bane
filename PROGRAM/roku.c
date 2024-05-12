/*
*
*
*
*
*
*
*
*
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MULTICAST_ADDR "239.255.255.250"
#define MULTICAST_PORT 1900

void discover()
{
  // Create a UDP socket
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    
    // Enable multicast TTL (Time-To-Live) for the socket
    int ttl = 1;
    if (setsockopt(sockfd, IPPROTO_IP, IP_MULTICAST_TTL, &ttl, sizeof(ttl)) < 0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    
    // Construct the multicast address structure
    struct sockaddr_in multicast_addr;
    memset(&multicast_addr, 0, sizeof(multicast_addr));
    multicast_addr.sin_family = AF_INET;
    multicast_addr.sin_addr.s_addr = inet_addr(MULTICAST_ADDR);
    multicast_addr.sin_port = htons(MULTICAST_PORT);
    
    // Construct the SDDP search message
    const char *search_msg = "M-SEARCH * HTTP/1.1\r\n"
                             "HOST: " MULTICAST_ADDR ":" STR(MULTICAST_PORT) "\r\n"
                             "MAN: \"ssdp:discover\"\r\n"
                             "ST: ssdp:all\r\n"
                             "MX: 1\r\n\r\n";
    
    // Send the search message as a multicast packet
    if (sendto(sockfd, search_msg, strlen(search_msg), 0, (struct sockaddr *)&multicast_addr, sizeof(multicast_addr)) < 0) {
        perror("sendto");
        exit(EXIT_FAILURE);
    }
    
    // Listen for responses from devices on the network
    char response[4096];
    ssize_t bytes_received;
    while ((bytes_received = recv(sockfd, response, sizeof(response) - 1, 0)) > 0) {
        response[bytes_received] = '\0';
        printf("Received response:\n%s\n", response);
    }
    
    // Close the socket
    close(sockfd);
    
    return 0;
}
