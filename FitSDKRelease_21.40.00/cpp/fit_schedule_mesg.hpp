////////////////////////////////////////////////////////////////////////////////
// The following FIT Protocol software provided may be used with FIT protocol
// devices only and remains the copyrighted property of Garmin Canada Inc.
// The software is being provided on an "as-is" basis and as an accommodation,
// and therefore all warranties, representations, or guarantees of any kind
// (whether express, implied or statutory) including, without limitation,
// warranties of merchantability, non-infringement, or fitness for a particular
// purpose, are specifically disclaimed.
//
// Copyright 2020 Garmin Canada Inc.
////////////////////////////////////////////////////////////////////////////////
// ****WARNING****  This file is auto-generated!  Do NOT edit this file.
// Profile Version = 21.40Release
// Tag = production/akw/21.40.00-0-g813c158
////////////////////////////////////////////////////////////////////////////////


#if !defined(FIT_SCHEDULE_MESG_HPP)
#define FIT_SCHEDULE_MESG_HPP

#include "fit_mesg.hpp"

namespace fit
{

class ScheduleMesg : public Mesg
{
public:
    class FieldDefNum final
    {
    public:
       static const FIT_UINT8 Manufacturer = 0;
       static const FIT_UINT8 Product = 1;
       static const FIT_UINT8 SerialNumber = 2;
       static const FIT_UINT8 TimeCreated = 3;
       static const FIT_UINT8 Completed = 4;
       static const FIT_UINT8 Type = 5;
       static const FIT_UINT8 ScheduledTime = 6;
       static const FIT_UINT8 Invalid = FIT_FIELD_NUM_INVALID;
    };

    ScheduleMesg(void) : Mesg(Profile::MESG_SCHEDULE)
    {
    }

    ScheduleMesg(const Mesg &mesg) : Mesg(mesg)
    {
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of manufacturer field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsManufacturerValid() const
    {
        const Field* field = GetField(0);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns manufacturer field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    FIT_MANUFACTURER GetManufacturer(void) const
    {
        return GetFieldUINT16Value(0, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set manufacturer field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    void SetManufacturer(FIT_MANUFACTURER manufacturer)
    {
        SetFieldUINT16Value(0, manufacturer, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of product field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsProductValid() const
    {
        const Field* field = GetField(1);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns product field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    FIT_UINT16 GetProduct(void) const
    {
        return GetFieldUINT16Value(1, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set product field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    void SetProduct(FIT_UINT16 product)
    {
        SetFieldUINT16Value(1, product, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of favero_product field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsFaveroProductValid() const
    {
        const Field* field = GetField(1);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        if( !CanSupportSubField( field, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_FAVERO_PRODUCT ) )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid(0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_FAVERO_PRODUCT);
    }


    ///////////////////////////////////////////////////////////////////////
    // Returns favero_product field
    ///////////////////////////////////////////////////////////////////////
    FIT_FAVERO_PRODUCT GetFaveroProduct(void) const
    {
        return GetFieldUINT16Value(1, 0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_FAVERO_PRODUCT);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set favero_product field
    ///////////////////////////////////////////////////////////////////////
    void SetFaveroProduct(FIT_FAVERO_PRODUCT faveroProduct)
    {
        SetFieldUINT16Value(1, faveroProduct, 0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_FAVERO_PRODUCT);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of garmin_product field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsGarminProductValid() const
    {
        const Field* field = GetField(1);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        if( !CanSupportSubField( field, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_GARMIN_PRODUCT ) )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid(0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_GARMIN_PRODUCT);
    }


    ///////////////////////////////////////////////////////////////////////
    // Returns garmin_product field
    ///////////////////////////////////////////////////////////////////////
    FIT_GARMIN_PRODUCT GetGarminProduct(void) const
    {
        return GetFieldUINT16Value(1, 0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_GARMIN_PRODUCT);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set garmin_product field
    ///////////////////////////////////////////////////////////////////////
    void SetGarminProduct(FIT_GARMIN_PRODUCT garminProduct)
    {
        SetFieldUINT16Value(1, garminProduct, 0, (FIT_UINT16) Profile::SCHEDULE_MESG_PRODUCT_FIELD_GARMIN_PRODUCT);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of serial_number field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsSerialNumberValid() const
    {
        const Field* field = GetField(2);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns serial_number field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    FIT_UINT32Z GetSerialNumber(void) const
    {
        return GetFieldUINT32ZValue(2, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set serial_number field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    void SetSerialNumber(FIT_UINT32Z serialNumber)
    {
        SetFieldUINT32ZValue(2, serialNumber, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of time_created field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsTimeCreatedValid() const
    {
        const Field* field = GetField(3);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns time_created field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    FIT_DATE_TIME GetTimeCreated(void) const
    {
        return GetFieldUINT32Value(3, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set time_created field
    // Comment: Corresponds to file_id of scheduled workout / course.
    ///////////////////////////////////////////////////////////////////////
    void SetTimeCreated(FIT_DATE_TIME timeCreated)
    {
        SetFieldUINT32Value(3, timeCreated, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of completed field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsCompletedValid() const
    {
        const Field* field = GetField(4);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns completed field
    // Comment: TRUE if this activity has been started
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL GetCompleted(void) const
    {
        return GetFieldENUMValue(4, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set completed field
    // Comment: TRUE if this activity has been started
    ///////////////////////////////////////////////////////////////////////
    void SetCompleted(FIT_BOOL completed)
    {
        SetFieldENUMValue(4, completed, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of type field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsTypeValid() const
    {
        const Field* field = GetField(5);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns type field
    ///////////////////////////////////////////////////////////////////////
    FIT_SCHEDULE GetType(void) const
    {
        return GetFieldENUMValue(5, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set type field
    ///////////////////////////////////////////////////////////////////////
    void SetType(FIT_SCHEDULE type)
    {
        SetFieldENUMValue(5, type, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Checks the validity of scheduled_time field
    // Returns FIT_TRUE if field is valid
    ///////////////////////////////////////////////////////////////////////
    FIT_BOOL IsScheduledTimeValid() const
    {
        const Field* field = GetField(6);
        if( FIT_NULL == field )
        {
            return FIT_FALSE;
        }

        return field->IsValueValid();
    }

    ///////////////////////////////////////////////////////////////////////
    // Returns scheduled_time field
    ///////////////////////////////////////////////////////////////////////
    FIT_LOCAL_DATE_TIME GetScheduledTime(void) const
    {
        return GetFieldUINT32Value(6, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

    ///////////////////////////////////////////////////////////////////////
    // Set scheduled_time field
    ///////////////////////////////////////////////////////////////////////
    void SetScheduledTime(FIT_LOCAL_DATE_TIME scheduledTime)
    {
        SetFieldUINT32Value(6, scheduledTime, 0, FIT_SUBFIELD_INDEX_MAIN_FIELD);
    }

};

} // namespace fit

#endif // !defined(FIT_SCHEDULE_MESG_HPP)
