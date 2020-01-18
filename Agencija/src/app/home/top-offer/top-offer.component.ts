import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-top-offer',
  templateUrl: './top-offer.component.html',
  styleUrls: ['./top-offer.component.scss']
})
export class TopOfferComponent implements OnInit {
  @Input('offer') offer: { title: string; description: string; image: string };

  constructor() {}

  ngOnInit() {}
}
