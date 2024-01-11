import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit{
  constructor(private route: Router){}
 
  ngOnInit(): void {

  }
  showSensor(sensorName:string){
    this.route.navigate(['device/' + sensorName])
  }


}
