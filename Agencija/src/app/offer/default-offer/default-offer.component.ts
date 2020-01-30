import { Component, OnInit, Input } from '@angular/core';
import { Offer } from '../../../core/VO/Offer';

@Component({
  selector: 'app-default-offer',
  templateUrl: './default-offer.component.html',
  styleUrls: ['./default-offer.component.scss']
})
export class DefaultOfferComponent implements OnInit {

  @Input() offer: Offer;

  constructor() {}

  ngOnInit() {}
}
