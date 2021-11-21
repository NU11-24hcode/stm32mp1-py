import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GrilleComponent } from './component/grille/grille.component';
import { WebSocketService } from './service/webSocket/web-socket.service';
import { WsConnectionService } from './service/WSconnection/ws-connection.service';

@NgModule({
  declarations: [
    AppComponent,
    GrilleComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [WsConnectionService,WebSocketService],
  bootstrap: [AppComponent]
})
export class AppModule { }
