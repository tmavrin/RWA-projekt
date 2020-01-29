import { ChangeDetectorRef, Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Offer } from '../../../core/VO/Offer';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { CoreService } from '../../../core/core.service';
/*
function requiredFileType(type: string) {
  return (control: FormControl) => {
    const file = control.value;
    if (!file) {
      return null;
    }

    const extension = file.name.split('.')[1].toLowerCase();
    if (type.toLowerCase() !== extension.toLowerCase()) {
      return {
        requiredFileType: true
      };
    } else {
      return null;
    }
  };
}
*/
@Component({
  selector: 'app-edit-offer',
  templateUrl: './edit-offer.component.html',
  styleUrls: ['./edit-offer.component.scss']
})
export class EditOfferComponent implements OnInit {
  // tslint:disable-next-line:no-input-rename
  @Input('offer') offer: Offer;
  @Output() collapse = new EventEmitter();
  editForm: FormGroup;
  showErrorMessage = false;
  image = null;
  pdf = null;

  constructor(protected formBuilder: FormBuilder,
              protected coreService: CoreService,
              protected cd: ChangeDetectorRef) {
    this.editForm = this.formBuilder.group({
     // image: ['', [requiredFileType('png')]],
      title: ['', [Validators.required]],
      description: ['', Validators.required],
      isTop: '',
      price: ['', Validators.required] // ,
    //  pdf: ['', [requiredFileType('pdf')]]
    });
  }

  ngOnInit() {
    this.editForm.get('title').setValue(this.offer.title);
    this.editForm.get('description').setValue(this.offer.description);
    this.editForm.get('isTop').setValue(this.offer.isTop);
    this.editForm.get('price').setValue(this.offer.price);
  }

  onFileChange(event, type) {
    if (type === 'pdf') {
      this.pdf = event.target.files[0];
      // console.log(this.pdf);
    } else if (type === 'png') {
      this.image = event.target.files[0];
      // console.log(this.image);
    }
  }

  submit() {
    if (this.editForm.invalid) {
      this.showErrorMessage = true;
      return;
    }

    this.offer.title = this.editForm.get('title').value;
    this.offer.description = this.editForm.get('description').value;
    this.offer.price = this.editForm.get('price').value;
    this.offer.isTop = this.editForm.get('isTop').value;
    this.offer.image = this.editForm.get('isTop').value;

  /*  this.coreService.editOffer(this.offer).subscribe(data => {
      console.log(data);
    }, error => { console.log(error.message); });
*/

    if (this.pdf !== null) {
      this.coreService.uploadPdf(this.offer.id, this.pdf).subscribe(data => {
        console.log(data);
      }, error => { console.log(error.message); });
    }
  }
}
