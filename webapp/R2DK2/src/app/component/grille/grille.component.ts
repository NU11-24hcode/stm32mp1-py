import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';


@Component({
  selector: 'app-grille',
  templateUrl: './grille.component.html',
  styleUrls: ['./grille.component.css']
})
export class GrilleComponent implements OnInit {



  constructor() {

  }

  @ViewChild('canvas', { static: true })
  canvas: ElementRef<HTMLCanvasElement>;

  private ctx: CanvasRenderingContext2D;

  ngOnInit(): void {
    this.ctx = this.canvas.nativeElement.getContext('2d');
    this.draw();
  }

  animate(): void {}
  draw() {
    const canvas = document.querySelector('#canvas');

    // set line stroke and line width
    this.ctx.strokeStyle = 'black';
    this.ctx.lineWidth = 2;


    this.ctx.beginPath();
    this.ctx.moveTo(100, 100);
    this.ctx.lineTo(300, 100);
    this.ctx.stroke();

}







}
