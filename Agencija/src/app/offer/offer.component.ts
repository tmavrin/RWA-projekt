import { Component, OnInit } from '@angular/core';
import { DUMMY_OFFERS } from '../VO/Offer';

@Component({
  selector: 'app-offer',
  templateUrl: './offer.component.html',
  styleUrls: ['./offer.component.scss']
})
export class OfferComponent implements OnInit {
  offers = DUMMY_OFFERS;

  constructor() {}

  ngOnInit() {}
}
