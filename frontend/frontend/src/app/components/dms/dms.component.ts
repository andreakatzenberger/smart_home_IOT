import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SmarthomeService } from 'src/app/services/smarthome.service';
import { SnackbarService } from 'src/app/services/snackbar.service';

@Component({
  selector: 'app-dms',
  templateUrl: './dms.component.html',
  styleUrls: ['./dms.component.css']
})
export class DmsComponent {
  hasError = false;
  errorValue = '';
  pinForm = new FormGroup(
    {
      pin: new FormControl('', [Validators.pattern(/^\d{4}(#)?$/), Validators.minLength(4), Validators.maxLength(5), Validators.required])

    }
  );
  deactivateSystem(){
    if(!this.pinForm.valid){
      this.hasError = true;
      const pinErrors = this.pinForm.controls.pin.errors;
      if (pinErrors?.['pattern']) {
        this.errorValue = 'Invalid format. Please enter 4 digits followed by an optional #.';
      } else if (pinErrors?.['minlength']) {
        this.errorValue = 'PIN must be at least 4 characters long.';
      } else if (pinErrors?.['maxlength']) {
        this.errorValue = 'PIN cannot be more than 5 characters long.';
      }
      return;
    }
    this.hasError = false;
    this.service.deactivate_system(this.pinForm.value.pin).subscribe({
      next:(res) =>{
        if(res['error']){
          this.hasError = true;
          this.errorValue = res['error'];
        }else{
          this.snackbar.showSnackBar('Successfully deactivated system.', 'Ok');

        }
      },
      error:(err) =>{
        this.hasError = true;
        this.errorValue = err.error;
      }
    })
  }
  submit(){
    if(!this.pinForm.valid){
      this.hasError = true;
      const pinErrors = this.pinForm.controls.pin.errors;
      if (pinErrors?.['pattern']) {
        this.errorValue = 'Invalid format. Please enter 4 digits followed by an optional #.';
      } else if (pinErrors?.['minlength']) {
        this.errorValue = 'PIN must be at least 4 characters long.';
      } else if (pinErrors?.['maxlength']) {
        this.errorValue = 'PIN cannot be more than 5 characters long.';
      }
      return;
    }
    this.hasError = false;
    this.service.activate_system(this.pinForm.value.pin).subscribe({
      next:(res) =>{ if(res['error']){
        this.hasError = true;
        this.errorValue = res['error'];
      }else{
        this.snackbar.showSnackBar('Successfully set system pin. Wait 10 seconds for it to be active.', 'Ok');

      }},
      error:(err) =>{
        this.hasError = true;
        this.errorValue = err.error;
      }
    })
  }
  constructor(private service: SmarthomeService, private snackbar: SnackbarService){}


}
