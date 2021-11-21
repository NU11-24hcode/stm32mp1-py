import { elementEventFullName } from "@angular/compiler/src/view_compiler/view_compiler";
import { strictEqual } from "assert";
import { Case } from 'src/app/class/case';

export class Labyrinthe {

  start:number[];
  end:number[];

  casesNb = [
    [2,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,0,0,1,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,1,0,0,1,0,0,0,1,0],
    [0,0,0,0,1,0,1,1,1,0],
    [0,1,0,0,1,0,0,0,1,0],
    [0,1,1,1,1,0,0,0,0,0],
    [0,1,0,0,1,1,1,1,0,0],
    [1,1,0,0,0,0,1,0,0,0],
    [0,0,0,3,0,0,0,0,0,0],
    []
  ];

  cases:Case[][]=Array(Array());



  startingCase:Case;
  starting_x_y:number[] = [0,0];
  endingCase:Case;
  ending_x_y:number[];
  currentCase:Case;
  current_x_y:number[] = [0,0];


  commands:number[] = Array();

  values:string[] =  ["Droite", "Gauche", "Haut", "Bas"];

  getCommandes () : String {
    let finalString = this.values[this.commands[0]];
    for(let i = 1; i<this.commands.length; i++){
      finalString+=" - "+this.values[this.commands[i]];
    }
    return finalString;
  }

  addCommand(nb){
    //this.commands.push(nb);


    console.log("i'm in "+this.current_x_y[0]+this.current_x_y[1])

    //this.currentCase = this.startingCase;

    var tempCurrent = [this.current_x_y[0], this.current_x_y[1]];

    switch(nb){
      case 0:
        tempCurrent[0]+=1;
        break;
      case 1:
        tempCurrent[0]-=1;
        break;
      case 2:
        tempCurrent[1]-=1;
        break;
      case 3:
        tempCurrent[1]+=1;
        break;
    }

    var caseValue = this.casesNb[tempCurrent[1]][tempCurrent[0]];


    if (caseValue==0){
      this.current_x_y = tempCurrent;
    }
    else if(caseValue==3){
      console.log("victoire!");
    }
    else{
      console.log("ne peut pas aller là");
    }




    this.commands.pop();
  }


}
