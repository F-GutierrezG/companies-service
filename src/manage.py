import sys
import click
import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db
from project.models import Company, UserCompanies, Classification


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/__init__.py',
    ]
)
COV.start()


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    db.session.add(Classification(name='Alimentos'))
    db.session.add(Classification(name='Bebidas No Alcohólicas'))
    db.session.add(Classification(name='Tabaco'))
    db.session.add(Classification(name='Estupefacientes'))
    db.session.add(Classification(name='Prendas de Vestir'))
    db.session.add(Classification(name='Calzado'))
    db.session.add(Classification(name='Arriendos Efectivos del Alojamiento'))
    db.session.add(Classification(name='Arriendos Imputados al Alojamiento'))
    db.session.add(Classification(name='Conservación y Reparación de la Vivienda'))
    db.session.add(Classification(name='Suministro de Agua y Servicios Relacionados con la Vivienda'))
    db.session.add(Classification(name='Electricidad, Gas Y Otros Combustibles'))
    db.session.add(Classification(name='Otros Muebles De Living N.C.P.'))
    db.session.add(Classification(name='Productos Textiles Para el Hogar'))
    db.session.add(Classification(name='Artefactos Para el Hogar'))
    db.session.add(Classification(name='Articulos de Vidrio y Cristal, Valija Y Utensilios Para El Hogar'))
    db.session.add(Classification(name='Herramientas y Equipo Para El Hogar Y El Jardín'))
    db.session.add(Classification(name='Bienes Y Servicios Para La Conservación Ordinaria Del Hogar'))
    db.session.add(Classification(name='Productos, Artefactos Y Equipos Médicos'))
    db.session.add(Classification(name='Servicios Para Pacientes Externos'))
    db.session.add(Classification(name='Servicios De Hospital'))
    db.session.add(Classification(name='Adquision De Vehículos'))
    db.session.add(Classification(name='Funcionamiento De Equipo De Transporte Personal'))
    db.session.add(Classification(name='Servicios De Transporte'))
    db.session.add(Classification(name='Servicios Postales'))
    db.session.add(Classification(name='Equipo Telefónico Y De Facsimile'))
    db.session.add(Classification(name='Servicios Telefónicos Y De Facsimile'))
    db.session.add(Classification(name='Equipo Audiovisual, Fotográfico Y De Procesamiento De Información'))
    db.session.add(Classification(name='Otros Bienes Durables Para El Ocio Y La Cultura'))
    db.session.add(Classification(name='Otros Articulos Y Equipo Para Recreción, Jardines Y Animales Domésticos'))
    db.session.add(Classification(name='Servicis De Recreación Y Culturales'))
    db.session.add(Classification(name='Periódicos, Libros Y Papeles, Y Útiles De Oficina'))
    db.session.add(Classification(name='Paquetes Turísticos'))
    db.session.add(Classification(name='Enseñanza Pre-Escolar Y Básica'))
    db.session.add(Classification(name='Enseñanza Secundaria'))
    db.session.add(Classification(name='Enseñanza Postsecundaria No Terciaria'))
    db.session.add(Classification(name='Enseñanza Terciaria'))
    db.session.add(Classification(name='Enseñanza No Atribuible A Ningún Nivel'))
    db.session.add(Classification(name='Servicios De Suministro De Comidas Por Contrato'))
    db.session.add(Classification(name='Servicios De Alojamiento'))
    db.session.add(Classification(name='Cuidados Personal'))
    db.session.add(Classification(name='Prostitución'))
    db.session.add(Classification(name='Efectos Personales N.E.P'))
    db.session.add(Classification(name='Protección Social'))
    db.session.add(Classification(name='Seguros'))
    db.session.add(Classification(name='Servicios Financieros N.C.P.'))
    db.session.add(Classification(name='Otros Servicios N.C.P.'))
    db.session.commit()

    company = Company(
        identifier="1", name="Compañia 1", classification=Classification.query.first())
    company.users.append(UserCompanies(user_id=1))

    db.session.add(company)
    db.session.commit()


@cli.command()
def clean_db():
    db.drop_all()
    db.session.commit()


@cli.command()
@click.option('--file', default=None)
def test(file):
    """Runs the tests without code coverage"""
    if file is None:
        tests = unittest.TestLoader().discover(
            'project/tests', pattern='test_*.py')
    else:
        tests = unittest.TestLoader().discover(
            'project/tests', pattern='{}.py'.format(file))

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    sys.exit(1)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    cli()
