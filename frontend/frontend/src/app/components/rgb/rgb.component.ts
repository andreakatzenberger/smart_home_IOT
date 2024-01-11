import { Component } from '@angular/core';
import { RgbColor } from 'src/app/model/device';
import { SmarthomeService } from 'src/app/services/smarthome.service';

@Component({
  selector: 'app-rgb',
  templateUrl: './rgb.component.html',
  styleUrls: ['./rgb.component.css']
})
export class RgbComponent {
  currentColor = 'none';
  colors : RgbColor[] = [
    {colorName:'none', colorValue: '0'},
    {colorName:'white', colorValue: '1'},
    {colorName:'red', colorValue: '2'},
    {colorName:'green', colorValue: '3'},
    {colorName:'blue', colorValue: '4'},
    {colorName:'lightblue', colorValue: '5'},
    {colorName:'purple', colorValue: '6'},
    {colorName:'yellow', colorValue: '7'},
  ];
  constructor(private service: SmarthomeService) {
    
  }
  setColor(colorValue:string){
    this.service.change_rgb_color(colorValue).subscribe(
      result =>{
        for(let col of this.colors){
          if (col.colorValue == colorValue){
            this.currentColor = col.colorName;
            break
          }

        }
  
      }
    )
  }
}
