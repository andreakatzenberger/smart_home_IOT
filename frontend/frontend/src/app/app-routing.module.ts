import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AlarmClockComponent } from './components/alarm-clock/alarm-clock.component';
import { HouseAlarmComponent } from './components/house-alarm/house-alarm.component';
import { HomeComponent } from './components/home/home.component';
import { DisplayDeviceComponent } from './components/display-device/display-device.component';
import { HouseStatusComponent } from './components/house-status/house-status.component';

const routes: Routes = [
  {path: 'alarm-clock', component: AlarmClockComponent},
  {path: 'house-alarm', component: HouseAlarmComponent},
  {path: 'device/:name', component: DisplayDeviceComponent},
  {path: 'house-status', component: HouseStatusComponent},
  { path: '', redirectTo: '', pathMatch: 'full'},
  { path: '**', component: HomeComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
