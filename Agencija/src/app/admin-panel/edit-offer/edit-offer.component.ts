import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Offer } from '../../../core/VO/Offer';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

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

  constructor(protected formBuilder: FormBuilder) {
    this.editForm = this.formBuilder.group({
      image: '',
      title: ['', [Validators.required]],
      description: ['', Validators.required],
      isTop: '',
      price: ['', Validators.required],
      pdf: ''
    });
  }

  ngOnInit() {
    this.editForm.get('title').setValue(this.offer.title);
    this.editForm.get('description').setValue(this.offer.description);
    this.editForm.get('isTop').setValue(this.offer.isTop);
    this.editForm.get('price').setValue(this.offer.price);
  }

  submit() {
    if (this.editForm.invalid) {
      this.showErrorMessage = true;
      return;
    }
  }
}
