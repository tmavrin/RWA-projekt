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

  @Input() offer: Offer;
  @Output() collapse = new EventEmitter();
  @Output() done = new EventEmitter();
  editForm: FormGroup;
  showErrorMessage = false;
  image = null;
  pdf = null;
  method = 'edit';

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
    if (this.offer.title !== '') {
      this.editForm.get('title').setValue(this.offer.title);
      this.editForm.get('description').setValue(this.offer.description);
      this.editForm.get('isTop').setValue(this.offer.isTop);
      this.editForm.get('price').setValue(this.offer.price);
      this.pdf = this.offer.pdf;
    } else {
      this.method = 'add';
    }
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

    if (this.method === 'edit') {
      this.editOffer();
    } else {
      this.addOffer();
    }

    if (this.pdf !== null) {
      this.coreService.uploadPdf(this.offer.id, this.pdf).subscribe(data => {
        console.log('good pdf :)', data);
      }, error => { console.log('bad pdf :('); });
    }

    if (this.image !== null) {
      this.coreService.uploadImage(this.offer.id, this.image).subscribe(data => {
        console.log('good image :)', data);
      }, error => { console.log('bad image :('); });
    }

    this.done.emit();
  }

  editOffer() {
    this.coreService.editOffer(this.offer).subscribe(data => {
      console.log('good offer :)', data);
    }, error => { console.log('bad offer :('); });
  }

  addOffer() {
    this.coreService.addOffer(this.offer).subscribe(data => {
      console.log('good offer :)', data);
    }, error => { console.log('bad offer :('); });
  }
}
