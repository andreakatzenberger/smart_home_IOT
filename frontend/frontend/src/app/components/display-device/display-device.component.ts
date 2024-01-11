import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-display-device',
  templateUrl: './display-device.component.html',
  styleUrls: ['./display-device.component.css']
})
export class DisplayDeviceComponent implements OnInit{
  name = '';
  measurementName = '';
  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.name = params['name'];
    });
    this.measurementName = this.getMeasurementName();
  }
  constructor(private route: ActivatedRoute){}
  getMeasurementName(): string{
    if(this.name == 'DS1') return 'Pressed';
    else if(this.name == 'DL') return 'Light';
    else if(this.name == 'DUS1') return 'Distance';
    else if(this.name == 'DB') return 'Buzz';
    else if(this.name == 'DPIR1') return 'Motion';
    else if(this.name == 'DMS') return 'Membrane';
    else if(this.name == 'RPIR1') return 'Motion';
    else if(this.name == 'RPIR2') return 'Motion';
    else if(this.name == 'RDHT1')  return 'dht'
    else if(this.name == 'RDHT2')  return 'dht'
    else if(this.name == 'DS2') return 'Pressed';
    else if(this.name == 'DUS2') return 'Distance';
    else if(this.name == 'DPIR2') return 'Motion';
    else if(this.name == 'GDHT') return 'dht';
    else if(this.name == 'GLCD') return 'Text';
    else if(this.name == 'GSG') return 'gyro';
    else if(this.name == 'RPIR3') return 'Motion';
    else if(this.name == 'RPIR4') return 'Motion';
    else if(this.name == 'RDHT4') return 'dht';
    else if(this.name == 'RDHT3') return 'dht';
    else if(this.name == 'BB') return 'Buzz';
    else if(this.name == 'B4SD') return 'B4SD Time';
    else if(this.name == 'BIR') return 'Motion';
    else if(this.name == 'BRGB') return 'RGB';
    return '';
  }

}
