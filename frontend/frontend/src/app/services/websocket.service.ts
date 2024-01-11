import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root',
})
export class WebsocketService {
  constructor(private socket: Socket) {}

  emit(event: string, data: any): void {
    // Send data to the server
    this.socket.emit(event, data);
  }

  listen(event: string): any {
    return this.socket.fromEvent(event);
  }
}