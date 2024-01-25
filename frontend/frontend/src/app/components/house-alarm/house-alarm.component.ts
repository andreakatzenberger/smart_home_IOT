import { Component, OnInit } from '@angular/core';
import { SmarthomeService } from 'src/app/services/smarthome.service';
import { SnackbarService } from 'src/app/services/snackbar.service';

@Component({
  selector: 'app-house-alarm',
  templateUrl: './house-alarm.component.html',
  styleUrls: ['./house-alarm.component.css']
})
export class HouseAlarmComponent  implements OnInit{
  alarmStatus = false;
  ngOnInit(): void {
    this.service.get_alarm_on().subscribe(
      result =>{
        this.alarmStatus = result['status'];
      }
    )
    
  }
  constructor(private service: SmarthomeService, private snack: SnackbarService){}
  deactivateButton(){
    this.service.deactivate_system_alarm().subscribe(
      result =>{
        this.snack.showSnackBar(result['response'], 'Ok');
      }
    )
  }
}
