import { Component, OnInit, Input } from '@angular/core';
import { Offer } from '../../VO/Offer';

@Component({
  selector: 'app-default-offer',
  templateUrl: './default-offer.component.html',
  styleUrls: ['./default-offer.component.scss']
})
export class DefaultOfferComponent implements OnInit {
  // tslint:disable-next-line:no-input-rename
  @Input('offer') offer: Offer;

  constructor() {}

  ngOnInit() {}
}