import { Component, OnInit } from '@angular/core';
import { DUMMY_OFFERS } from '../VO/Offer';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  topOffers = DUMMY_OFFERS;

  constructor() {}

  ngOnInit() {}
}
