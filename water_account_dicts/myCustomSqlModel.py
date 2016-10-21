# -*- coding: utf-8 -*-
__author__ = 'POLTAROKOV SP'


from PyQt4 import QtCore, QtGui, QtSql, Qt

class myCustomSqlModel(QtSql.QSqlQueryModel):
    def __init__(self, QObject_parent=None):
        super(myCustomSqlModel, self).__init__(QObject_parent)

    def flags(self, QModelIndex):
        #Qt::ItemFlags flags = QSqlQueryModel::flags(index);
        #if (index.column() == 1 || index.column() == 2)
        #    flags |= Qt::ItemIsEditable;
        #return flags;
        super(myCustomSqlModel, self).flags(QModelIndex)

    #def __init__(self, parent=None):
    #   QtSql.QSqlQueryModel.__init__(self,parent)

    def setData(self, QModelIndex, p_object, int_role=None):
        #if (index.column() < 1 || index.column() > 2)
            #return false;

        #QModelIndex primaryKeyIndex = QSqlQueryModel::index(index.row(), 0);
        #int id = data(primaryKeyIndex).toInt();

        #clear();

        #bool ok;

        #if (index.column() == 1) {
        #ok = setStrData(id, value.toString());
        #} else {
        #ok = setStrData(id, value.toString());}
        #refresh();
        #return ok;

        return super(myCustomSqlModel, self).setData(QModelIndex, p_object, int_role)

    def refresh(self):
        self.setQuery("SELECT * FROM...")
        self.setHeaderData(0, QtCore.Qt.Horizontal, "ID")

    def setStrData(self, objId, strData):
        setQ = QtSql.QSqlQuery()
        setQ.prepare("update person set firstname = ? where id = ?")
        setQ.bindValue(strData)
        return setQ.exec_()

    def data(self, QModelIndex, int_role=None):
        #QVariant value = QSqlQueryModel::data(index, role);
        #if (value.isValid() && role == Qt::DisplayRole) {
        #if (index.column() == 0)
        #return value.toString().prepend("#");
        #else if (index.column() == 2)
            #return value.toString().toUpper();}
        #if (role == Qt::TextColorRole && index.column() == 1)
            #return QVariant::fromValue(QColor(Qt::blue));
        #return value;
        return super(myCustomSqlModel, self).data(QModelIndex, int_role)

#include <QtWidgets>
#include <QtSql>

#include "../connection.h"

# void initializeModel(QSqlRelationalTableModel *model)
# {
#     model->setTable("employee");
#
#     model->setEditStrategy(QSqlTableModel::OnManualSubmit);
#     model->setRelation(2, QSqlRelation("city", "id", "name"));
#     model->setRelation(3, QSqlRelation("country", "id", "name"));
#
#     model->setHeaderData(0, Qt::Horizontal, QObject::tr("ID"));
#     model->setHeaderData(1, Qt::Horizontal, QObject::tr("Name"));
#     model->setHeaderData(2, Qt::Horizontal, QObject::tr("City"));
#     model->setHeaderData(3, Qt::Horizontal, QObject::tr("Country"));
#
#     model->select();
# }
#
# QTableView *createView(const QString &title, QSqlTableModel *model)
# {
#     QTableView *view = new QTableView;
#     view->setModel(model);
#     view->setItemDelegate(new QSqlRelationalDelegate(view));
#     view->setWindowTitle(title);
#     return view;
# }
#
# void createRelationalTables()
# {
#     QSqlQuery query;
#     query.exec("create table employee(id int primary key, name varchar(20), city int, country int)");
#     query.exec("insert into employee values(1, 'Espen', 5000, 47)");
#     query.exec("insert into employee values(2, 'Harald', 80000, 49)");
#     query.exec("insert into employee values(3, 'Sam', 100, 1)");
#
#     query.exec("create table city(id int, name varchar(20))");
#     query.exec("insert into city values(100, 'San Jose')");
#     query.exec("insert into city values(5000, 'Oslo')");
#     query.exec("insert into city values(80000, 'Munich')");
#
#     query.exec("create table country(id int, name varchar(20))");
#     query.exec("insert into country values(1, 'USA')");
#     query.exec("insert into country values(47, 'Norway')");
#     query.exec("insert into country values(49, 'Germany')");
# }
#
# int main(int argc, char *argv[])
# {
#     QApplication app(argc, argv);
#     if (!createConnection())
#         return 1;
#     createRelationalTables();
#
#     QSqlRelationalTableModel model;
#
#     initializeModel(&model);
#
#     QTableView *view = createView(QObject::tr("Relational Table Model"), &model);
#     view->show();
#
#     return app.exec();
# }


