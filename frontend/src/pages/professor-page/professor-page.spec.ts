import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfessorPage } from './professor-page';

describe('ProfessorPage', () => {
  let component: ProfessorPage;
  let fixture: ComponentFixture<ProfessorPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProfessorPage],
    }).compileComponents();

    fixture = TestBed.createComponent(ProfessorPage);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
