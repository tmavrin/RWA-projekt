import { Component, OnInit, Input } from '@angular/core';
import { Offer } from '../../../core/VO/Offer';

@Component({
  selector: 'app-top-offer',
  templateUrl: './top-offer.component.html',
  styleUrls: ['./top-offer.component.scss']
})
export class TopOfferComponent implements OnInit {
  // tslint:disable-next-line:no-input-rename
  @Input('offer') offer: Offer;

  constructor() {}

  ngOnInit() {}
}
