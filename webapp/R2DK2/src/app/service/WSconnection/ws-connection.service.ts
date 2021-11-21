import { Injectable } from '@angular/core';
import { Subject } from "rxjs";
import {map} from 'rxjs/operators';
import { WebSocketService } from '../webSocket/web-socket.service';

const SERVER_URL = "ws://127.0.0.1:8080"

export interface Message {
  data: string;
}

@Injectable({
  providedIn: 'root'
})
export class WsConnectionService {

  public messages: Subject<Message>;

  constructor(wsService: WebSocketService) {
    this.messages = <Subject<Message>>wsService.connect(SERVER_URL).pipe(
    map((response: MessageEvent): Message => {
        let data = JSON.parse(response.data);
        return {data:data};
      })
    );
  }
}
