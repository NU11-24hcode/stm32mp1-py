import { Component } from '@angular/core';
import { Labyrinthe } from 'src/app/class/labyrinthe';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  lab : Labyrinthe;
  title = 'R2DK2';
  constructor(){
    this.lab = new Labyrinthe();
  }
}
