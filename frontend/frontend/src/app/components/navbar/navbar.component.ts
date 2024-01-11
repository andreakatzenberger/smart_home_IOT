
import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../../services/websocket.service';
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit{

  message = '';
  receivedMessage = '';

  constructor(private websocketService: WebsocketService) {}

  ngOnInit(): void {
    this.websocketService.listen('message_from_server').subscribe((message: string) => {
      this.receivedMessage = message;
      console.log(this.receivedMessage)
    });
  }

  sendMessage(): void {
    // Send a message to the server
    this.websocketService.emit('message_from_client', this.message);
  }

 

}
